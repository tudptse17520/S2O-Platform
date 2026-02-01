"""
QR Code Generation Service for S2O Platform
Generates QR codes for tables, payments, and menu access
"""
import io
import base64
from typing import Optional, Dict, Any

try:
    import qrcode
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False


class QRCodeService:
    """Service for generating QR codes"""
    
    def __init__(self, base_url: str = "https://s2o.app"):
        self.base_url = base_url
    
    def generate_table_qr(
        self, 
        tenant_id: str, 
        branch_id: str, 
        table_id: str,
        table_number: str = None
    ) -> Dict[str, Any]:
        """
        Generate QR code for table menu access
        
        Returns:
            Dict with:
            - qr_data: The URL encoded in the QR
            - qr_image_base64: Base64 encoded PNG image
            - qr_image_svg: SVG string (if available)
        """
        # Build the table order URL
        qr_url = f"{self.base_url}/order/{tenant_id}/{branch_id}/{table_id}"
        
        return self._generate_qr(
            data=qr_url,
            metadata={
                "type": "table_menu",
                "tenant_id": tenant_id,
                "branch_id": branch_id,
                "table_id": table_id,
                "table_number": table_number
            }
        )
    
    def generate_payment_qr(
        self,
        tenant_id: str,
        order_id: str,
        amount: float,
        bank_id: str = None,
        account_number: str = None
    ) -> Dict[str, Any]:
        """
        Generate VietQR payment code
        
        For VietQR format: https://vietqr.net/portal-service/guide
        """
        # Build payment URL or VietQR data
        if bank_id and account_number:
            # VietQR format
            qr_data = self._build_vietqr_data(
                bank_id=bank_id,
                account_number=account_number,
                amount=amount,
                description=f"S2O-{order_id[:8]}"
            )
        else:
            # Internal payment URL
            qr_data = f"{self.base_url}/pay/{tenant_id}/{order_id}"
        
        return self._generate_qr(
            data=qr_data,
            metadata={
                "type": "payment",
                "tenant_id": tenant_id,
                "order_id": order_id,
                "amount": amount
            }
        )
    
    def generate_restaurant_qr(
        self,
        tenant_id: str,
        branch_id: str = None
    ) -> Dict[str, Any]:
        """Generate QR code for restaurant/branch info page"""
        if branch_id:
            qr_url = f"{self.base_url}/restaurant/{tenant_id}/branch/{branch_id}"
        else:
            qr_url = f"{self.base_url}/restaurant/{tenant_id}"
        
        return self._generate_qr(
            data=qr_url,
            metadata={
                "type": "restaurant_info",
                "tenant_id": tenant_id,
                "branch_id": branch_id
            }
        )
    
    def generate_loyalty_qr(
        self,
        tenant_id: str,
        customer_id: str
    ) -> Dict[str, Any]:
        """Generate QR code for customer loyalty card"""
        qr_url = f"{self.base_url}/loyalty/{tenant_id}/{customer_id}"
        
        return self._generate_qr(
            data=qr_url,
            metadata={
                "type": "loyalty_card",
                "tenant_id": tenant_id,
                "customer_id": customer_id
            }
        )
    
    def _generate_qr(
        self, 
        data: str, 
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Generate QR code image
        
        Returns dict with base64 image and metadata
        """
        result = {
            "qr_data": data,
            "metadata": metadata or {},
            "qr_image_base64": None,
            "qr_image_svg": None
        }
        
        if not QRCODE_AVAILABLE:
            # Return data only if qrcode library not installed
            result["error"] = "QR code library not available"
            return result
        
        try:
            # Create QR code with styling
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            # Generate PNG image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            result["qr_image_base64"] = base64_image
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _build_vietqr_data(
        self,
        bank_id: str,
        account_number: str,
        amount: float,
        description: str = ""
    ) -> str:
        """
        Build VietQR format data string
        
        Based on VietQR EMV QR Code specification
        """
        # Simplified VietQR URL format
        # Full EMV format would require more complex encoding
        amount_str = str(int(amount))
        desc_encoded = description.replace(" ", "%20")[:25]
        
        return (
            f"https://img.vietqr.io/image/{bank_id}-{account_number}-compact.png"
            f"?amount={amount_str}&addInfo={desc_encoded}"
        )


# Convenience functions
def generate_table_qr_code(
    tenant_id: str,
    branch_id: str,
    table_id: str,
    table_number: str = None,
    base_url: str = "https://s2o.app"
) -> Dict[str, Any]:
    """Quick function to generate table QR code"""
    service = QRCodeService(base_url)
    return service.generate_table_qr(tenant_id, branch_id, table_id, table_number)


def generate_payment_qr_code(
    tenant_id: str,
    order_id: str,
    amount: float,
    bank_id: str = None,
    account_number: str = None,
    base_url: str = "https://s2o.app"
) -> Dict[str, Any]:
    """Quick function to generate payment QR code"""
    service = QRCodeService(base_url)
    return service.generate_payment_qr(tenant_id, order_id, amount, bank_id, account_number)
